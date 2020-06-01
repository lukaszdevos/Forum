$('.btn-edit-comment').on('click', function(event) {
    event.preventDefault();
    var id = this.id.split('btn-edit-comment-')[1];
    var commentTextArea = $('#comment-edit-' + id);
    var commentContent = $('#comment-content-' + id);
    var buttonSave = $('#btn-save-comment-' + id);
    commentTextArea.toggleClass('hidden');
    commentContent.toggleClass('hidden');
    buttonSave.toggleClass('hidden');
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})