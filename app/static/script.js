// The script here is used in "base.html"
let content = document.getElementById('content');
$('#content-toggle').click( function(){
    $(content).fadeOut(1000);
});

// The script here is used in "index.html" 
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

let table = new DataTable('#the-index', {
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

table.on('click', 'tbody th.dt-control', function (e) {
    let tr = e.target.closest('tr');
    let row = table.row(tr);

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


// The script here is used in "add.html"
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
        // This error happens when not viewing the artist adding page, fine to ignore
    };
}, false);

// The script here is used in artist.html
window.onload = () => {
    try {
        const deleteModal = new bootstrap.Modal('#delete-modal');
        if (document.getElementById('delete-modal').getAttribute('title')) {
            deleteModal.show();
        };
    } catch(error) {
        // This error happens when not viewing the artist details page, fine to ignore
    };
}