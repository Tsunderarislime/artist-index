// The script here is used in all pages with the button that returns you to the top of the page
const topButton = document.getElementById("top-button");
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        $('#top-button').fadeIn(200);
    } else {
        $('#top-button').fadeOut(200);
    }
}

// The script here is used in multiple pages with tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// The script here is used in "index/index.html" 
try {
    function formatData(d) {
        let header = '<div class="slider" style="display: none;">' +
            '<table class="table table-striped table-bordered table-hover">'
        let links = ''
        let dict = JSON.parse(d[2]);

        for (const [key, value] of Object.entries(dict)) {
            links += '<tr>' +
                '<th scope="row" style="width: 20%;">' + key + '</th>' +
                '<td style="width: auto;"><a href="' + value + '">' + value + '</a></td>' +
                '</tr>'
        };

        return header + links +
            '</table>' +
            '</div>';
    }

    let indexTable = new DataTable('#the-index', {
        // 0 = name, 1 = searchable_name, 2 = social_media_links
        order: [[0, 'asc']],
        columnDefs: [
            {
                targets: [1, 2],
                visible: false,
                searchable: true
            }
        ],
        lengthMenu: [10, 20, 40]
    });

    indexTable.on('click', 'tbody th.dt-control', function (e) {
        let tr = e.target.closest('tr');
        let row = indexTable.row(tr);

        // 'do-not-scroll' class prevents table from sliding when clicking the link as an admin.
        if (!(e.target.classList.contains('do-not-scroll'))) {
            if ( row.child.isShown() ) {
                $('div.slider', row.child()).slideUp(250, function () {
                    row.child.hide();
                });
            }
            else {
                row.child(formatData(row.data()), 'no-padding' ).show();
                $('div.slider', row.child()).slideDown(250);
            };
        };
    });
} catch(error) {
    {};
};


// The script here is used in "artist/addeditartist.html"
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

// The script here is used in "artist/artist.html"
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

// The script here is used in "art/browse.html"
try {
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
} catch(error) {
    {};
}

// The script here is used in "info/about.html"
try {
    let content = document.getElementById('content');
    $('#content-toggle').click( function(){
        $(content).fadeOut(1000);
    });
} catch(error) {
    {};
}
