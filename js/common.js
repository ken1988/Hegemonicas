/**
 *
 */
 $(document).ready(function() {
	 $('#open_world_form').submit(function(event) {
		 //通常送信キャンセル
		 event.preventDefault();

         // 操作対象のフォーム要素を取得
		 var $form = $(this);
		 $.post($form.attr('action'),
			    $form.serialize(),
			    function(data){
			 alert("ERROR CODE:" + data);
		 })
	 })

 }