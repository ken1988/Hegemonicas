/**
 *
 */
 $(document).ready(function() {
	 $('.open_world_form').click(function() {
       //操作対象のフォーム要素を取得
		 var $form = $(this);
		 $.post($form.attr('action'),
			    $form.serialize())
			    .done(function(data) {
			    	var jsonData = data
			    	if (jsonData.code != 0){
			    		$('header').after(jsonData.msg);
			    	}else{
			    		$form.find(':hidden[name="mode"]').val('validated');
			    		$form.submit();
			    	}
		 });
	 });
 });