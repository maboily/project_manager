module.exports = function () {
    function getDeleteButtons() {
        return document.querySelectorAll('.confirm-delete');
    }

    function tagDeleteButtons() {
        getDeleteButtons().forEach((button) => {
            button.addEventListener('click', confirmDeletionDialog);
        });
    }

    function confirmDeletionDialog(evt) {
        if (!confirm('Are you sure you wish to delete the selected element?')) {
            evt.preventDefault();
        }
    }

    window.addEventListener('load', tagDeleteButtons);
};