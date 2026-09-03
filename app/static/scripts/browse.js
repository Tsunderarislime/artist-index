const browseModal = document.getElementById('browse-modal');
browseModal.addEventListener('show.bs.modal', function (event) {
    const clickedImage = event.relatedTarget;
    
    const imageLink = clickedImage.getAttribute('src');
    const imageArtist = clickedImage.getAttribute('data-art-artist')
    const imageSource = clickedImage.getAttribute('data-art-source')
    
    const modalImageTarget = document.getElementById('browse-modal-image');
    const modalImageGlowTarget = document.getElementById('browse-modal-image-glow');
    const modalArtistTarget = document.getElementById('browse-modal-artist');
    const modalSourceTarget = document.getElementById('browse-modal-source');
    
    modalImageTarget.src = imageLink;
    modalImageGlowTarget.src = imageLink;
    modalArtistTarget.href = "artist/" + imageArtist;
    modalArtistTarget.textContent = imageArtist;
    modalSourceTarget.href = imageSource;
    modalSourceTarget.textContent = imageSource;
});

Promise.all(Array.from(document.images)
    .filter(img => !img.complete)
    .map(img => new Promise(resolve => { img.onload = img.onerror = resolve; })))
    .then(() => {
        var msnry = new Masonry('#masonry-grid');
        msnry.layout();
        $('#loader-container').hide();
        $('#masonry-grid').animate({
            opacity: 1
        }, 1000);
});
