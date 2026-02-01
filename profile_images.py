import os
import sqlalchemy as sa
from app.models import Artist
from app import app, db
from xdk import Client

def main():
    basedir = os.path.abspath(os.path.dirname(__file__))
    hundred_file = os.path.join(basedir, 'hundred.txt')
    with app.app_context():
        total_rows = db.session.scalar(
            sa.Select(sa.func.count()).select_from(Artist)
        )

        # Handle which slice of 100 artists to read (0-99), (100-199), (200-299) by saving 0, 1, 2 to a file such that it loops like 0, 1, 2, 0, 1, 2, ...
        # Necessary since the X API limits number of queried usernames to 100 per query and only allows one query every 24 hours
        with open(hundred_file, 'r+') as f:
            current_slice = int(f.readline())
            next_slice = (current_slice + 1) % (total_rows // 100 + 1)
            
            f.seek(0)
            f.write(str(next_slice))
            f.truncate()
            f.close()
        
        start = 100 * current_slice
        end = start + 100

        artists = db.session.scalars(
            sa.Select(Artist).slice(start, end)
        ).all()

        profile_images = {}

        for artist in artists:
            if 'Twitter' in artist.social_media_links:
                profile_images[artist.id] = artist.social_media_links['Twitter'].split('/')[-1]

        bearer_token = os.environ.get('BEARER_TOKEN')
        client = Client(bearer_token=bearer_token)

        try:
            response = client.users.get_by_usernames(
                usernames=list(profile_images.values()),
                user_fields=['profile_image_url']
            )
            
            response_data = getattr(response, 'data', None)
            
            if response_data:
                urls = []
                for user in response_data:
                    urls.append(user['profile_image_url'])
                
                for key, url in zip(list(profile_images.keys()), urls):
                    profile_images[key] = url.replace('_normal', '')

                db.session.execute(
                    sa.Update(Artist).where(Artist.id.in_(list(profile_images.keys()))).values(
                        twitter_profile_image_url=sa.case(
                            profile_images,
                            value=Artist.id,
                            else_=""
                        )
                    )
                )

                db.session.commit()
            else:
                print("Failed to get a response from the Twitter endpoint. Skipping profile image updates.")

        except Exception as e:
            app.logger.error(e)

if __name__ == "__main__":
    main()