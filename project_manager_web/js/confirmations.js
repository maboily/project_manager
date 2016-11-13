export default {
    getDeleteButtons() {
        return document.querySelectorAll('.confirm-delete');
    },

    tagDeleteButtons() {
        this.getDeleteButtons().forEach((button) => {
            button.addEventListener('click', this.confirmDeletionDialog.bind(this));
        });
    },

    confirmDeletionDialog(evt) {
        if (!confirm('Are you sure you wish to delete the selected element?')) {
            evt.preventDefault();
        }
    },

    init() {
        window.addEventListener('load', this.tagDeleteButtons.bind(this));
    }
};