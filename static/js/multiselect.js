$(function(){
            var slidedown = false;
            $('.country').click(function(){
            if(!slidedown){
                $(this).removeClass('dot');
                slidedown = true;
            }else{
                  $(this).addClass('dot');
                  slidedown = false;
            }
            })
        })
        $(document).ready(function() {
            $('#category').multiselect({
                enableFiltering: true,
                includeSelectAllOption: true,
                maxHeight: 400,
                dropDown: true,
                buttonWidth: '120px',
                numberDisplayed: 1,
                checkboxName: 'catsel[]'
            });
        });
        $(document).ready(function() {
            $('#country').multiselect({
                enableFiltering: true,
                includeSelectAllOption: true,
                maxHeight: 400,
                dropDown: true,
                buttonWidth: '120px',
                numberDisplayed: 1,
                checkboxName: 'cousel[]'
            }
            );
        });