function formatData(d) {
    let header = '<div class="slider" style="display: none;">' +
        '<table class="table table-striped table-bordered table-hover">'
    let links = ''
    let dict = JSON.parse(d[2]);

    for (const [key, value] of Object.entries(dict)) {
        links += '<tr>' +
            '<th scope="row" style="width: 20%;">' + key + '</th>' +
            '<td style="width: auto;"><a href="' + value + '" target="_blank" rel="noopener noreferrer">' + value + '</a></td>' +
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
