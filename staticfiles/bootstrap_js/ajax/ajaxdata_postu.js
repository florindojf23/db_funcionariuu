
$(document).ready(function(){
    $('#id_munisipiu').on('change', function(){
        let munID = $(this).val();
        console.log(munID);
        if(munID){
            $.ajax({
                type:'POST',
                url:'ajax/ajaxdata_postu.php',
                data:'munid='+munID,
                success:function(html){
                    $('#id_postu').html(html);
                },
            }); 
        }else{
            $('#id_postu').html('<option value="">Select Munisipiu first</option>');
        }
    });


    $('#id_postu').on('change', function(){
        let postuID = $(this).val();
        console.log(postuID);
        if(postuID){
            $.ajax({
                type:'POST',
                url:'ajax/ajaxdata_postu.php',
                data:'postuid='+postuID,
                success:function(html){
                    $('#id_suku').html(html);
                },
            }); 
        }else{
            $('#id_suku').html('<option value="">Select Postu first</option>');
        }
    });
	
	
});
