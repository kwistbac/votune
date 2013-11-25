$(function()
{
	$(document).on('click', "#library", function(e)
	{
		e.preventDefault();
		
		$('<div>').attr('id', 'libraryModal')
		          .addClass('modal')
		          .addClass('fade')
		          .on('hidden.bs.modal', function(){ $(this).remove(); })
		          .modal({ remote: $(this).attr('href') });
		
	}).on('click', "#libraryAdd", function(e)
	{
		e.preventDefault();
		
		$('<div>').attr('id', 'libraryAddModal')
		          .addClass('modal')
		          .addClass('fade')
		          .on('hidden.bs.modal', function(){ $(this).remove(); })
		          .modal({ remote: $(this).attr('href') });
		
	}).on('click', "#libraryEdit", function(e)
	{
		e.preventDefault();
		
		$('<div>').attr('id', 'libraryEditModal')
		          .addClass('modal')
		          .addClass('fade')
		          .on('hidden.bs.modal', function(){ $(this).remove(); })
		          .modal({ remote: $(this).attr('href') });
		
	}).on('click', "#libraryRemove", function(e)
	{
		e.preventDefault();
		
		$('<div>').attr('id', 'libraryRemoveModal')
		          .addClass('modal')
		          .addClass('fade')
		          .on('hidden.bs.modal', function(){ $(this).remove(); })
		          .modal({ remote: $(this).attr('href') });
		
	});

});