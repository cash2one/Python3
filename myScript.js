function empty_form ()

	{
	    var txt = document.getElementsByClassName("user_input");

	    if (txt[0].value == '' || txt[1].value == '' || txt[2].value == '')
	    {
	        alert('Вы забыли ввести текст.');

	        return false;
	    }   
	    return true;
	}
