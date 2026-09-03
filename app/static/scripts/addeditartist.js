function addLink() {
    const firstLink = document.querySelector('.link-field');
    const newLink = document.createElement('div');
    newLink.classList.add('link-field');
    newLink.innerHTML = firstLink.innerHTML;

    const newIndex = document.querySelectorAll('.link-field').length;

    const social_media = newLink.querySelector('#social_media_links-0-social_media');
    social_media.id = `social_media_links-${newIndex}-social_media`;
    social_media.name = social_media.id;
    social_media.value = '';

    const link = newLink.querySelector('#social_media_links-0-link');
    link.id = `social_media_links-${newIndex}-link`;
    link.name = link.id;
    link.value = '';

    const button = newLink.querySelector('.delete-link-button');
    button.classList.remove('d-none');

    document.getElementById('link-fields').appendChild(newLink);
    document.querySelector('.link-field:last-child input').focus();
    return false;
}

function removeLink(e) {
    e.parentElement.parentElement.parentElement.remove();
}

document.addEventListener('DOMContentLoaded', function () {
    try {
        const firstLink = document.querySelector('.link-field');
        const firstButton = firstLink.querySelector('.delete-link-button');

        firstButton.classList.add('d-none');
    } catch(error) {
        {};
    };
}, false);
