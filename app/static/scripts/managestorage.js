function checkbox(e) {
    const checkbox = e.previousElementSibling;
    const row = checkbox.closest('tr');
    checkbox.checked = !checkbox.checked;
    row.classList.toggle('table-info');
};

const storageTable = document.getElementById('storage-table');
const selectedImages = document.getElementById('selected-images');
const selectedCountText = document.getElementById('selected-counter');
try {
    storageTable.addEventListener('click', () => {
        const count = storageTable.querySelectorAll('.image-checkbox:checked').length;
        if (count < 1) {
            selectedImages.style.display = 'none';
        } else if (count == 1) {
            selectedImages.style.display = 'block';
            selectedCountText.innerText = '1 image selected.';
        } else {
            selectedImages.style.display = 'block';
            selectedCountText.innerText = count + ' images selected.';
        }
    });
} catch (error) {
    console.log('Nothing to display.');
}


function loadIDs() {
    const idForm = document.getElementById('ids');
    const checked = storageTable.querySelectorAll('.image-checkbox:checked');
    let ids = [];

    idForm.value = '';
    
    checked.forEach(c => {
        ids.push(c.getAttribute('data-art-id'));
    });

    idForm.value = ids.join(',');
}

document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
});
