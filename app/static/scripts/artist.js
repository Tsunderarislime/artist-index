window.onload = () => {
    try {
        const deleteModal = new bootstrap.Modal('#delete-modal');
        const artUploadModal = new bootstrap.Modal('#art-upload-modal');
        const x = new bootstrap.Carousel('#art-carousel');

        if (document.getElementById('delete-modal').getAttribute('title')) {
            deleteModal.show();
        };
        if (document.getElementById('art-upload-modal').getAttribute('title')) {
            artUploadModal.show();
        };
    } catch(error) {
        {};
    };
}
