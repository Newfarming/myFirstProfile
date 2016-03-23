var saveCallback = function( res ){
        $('#JS_submit_toreport').attr('disabled' , false);
        if( res && ( res.status == 'ok' || res.status == 'success' ) ){
            var url = $('#JS_header').attr( 'data-url' );
            if( url ){
                location.href = url;
            }else{
                location.reload();
            };
        }else{
            if( res && res.msg ){
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>' + res.msg + '</p>');
            }else{
                $.alert('<p style="text-align:center;font-size:16px;"><i class="i-l-notice"></i>请求失败了，刷新再试一下吧！</p>');
            };
        };
    };
$(function(){

    $( document ).on( 'click' , '.m-radio', function(){
        var $this = $( this ),
            name = $this.attr('data-name'),
            hasInfo = $this.attr('has-info')
            checkbox = $this.find('input'),
            checked = checkbox.prop('checked'),
            $submitToReport = $('#JS_submit_toreport'),
            $feedbackInfo = $('#JS_feedback_info');

        $this.toggleClass('active');
        $('.m-radio[data-name="' + name + '"]').not( $this ).removeClass( 'active' ).find('input').prop('checked',false);
        checkbox.prop( 'checked' , !checked );

        if( name == 'code_name' ){
            if( $('input[name="code_name"]:checked').length ){
                $('#JS_submit_btn').attr('disabled' , false);
            }else{
                $('#JS_submit_btn').attr('disabled' , true);
            };
        };

        if( name == 'back_count' ){
            if (hasInfo === undefined) {
                $feedbackInfo.hide();
                if( $('input[name="back_count"]:checked').length ){
                    $submitToReport.attr('disabled' , false);
                }else{
                    $submitToReport.attr('disabled' , true);
                };
            } else {
                $feedbackInfo.toggle().find('input').focus();
                $submitToReport.attr('disabled' , true);
            }
        };

    });

    $(document).on('keyup', '#JS_feedback_value', function(){
        var $this = $(this),
            value = $this.val(),
            $submitToReport = $('#JS_submit_toreport');
        value === '' ? $submitToReport.attr('disabled' , true) : $submitToReport.attr('disabled' , false);
    });

    $(document).on('click','#JS_submit_btn',function(){
        var that = this;
        if( $(this).attr('disabled') ) return false;
        var txt = $('input[name="code_name"]:checked').parent().text();
        if( !txt ) return false;
        $.confirm('<p style="font-size:20px;color:#434343;text-align:center"><i class="i-l-notice"></i>您选择的状态是: <span style="color:#3ab2e7;">' + txt + '</span></p><p style="margin-top:50px;color:#f23748;font-size:14px;text-align:center;">注：请确认提交，提交后不能修改</p>' , function(){
            $.commonAjax.call( that );
        });

    });

    $( document ).on( 'click' , '#JS_toreport_btn' , function(){
        $('.modal-backdrop-tip-toreport,.modal-tip-toreport').show();
        $('.modal-dialog-tip-toreport').css({
            marginTop: ( $(window).height() - $('.modal-dialog-tip-toreport').height() ) / 2 + 'px'
        });
    });

    $( document ).on( 'click' , '.JS_close_tip' , function(){
        $('.modal-backdrop-tip-toreport,.modal-tip-toreport').hide();
    });

    $( document ).on( 'click' , '#JS_submit_toreport' , function(){
        var $this = $( this ),
            id = $this.attr( 'data-id' ),
            back_id = $('input[name="back_count"]:checked').val(),
            feedback_value = $('input[name="feedback_value"]').val();
        if( $(this).attr('disabled') ) return false;
        if( !id || !back_id ) return;
        $('#JS_submit_toreport').attr('disabled' , true);
        $.post( '/taocv/add_feedback/' , {
            feedback_id: back_id,
            resume_id: id,
            feedback_value: feedback_value,
            ___: new Date().getTime()
        } , function( res ){
            saveCallback( res );
        } ,'json' );

    });

    $( document ).on( 'click' , '#JS_goto_detail' , function(){
        var newWin = window.open();
        newWin.opener = null;
        newWin.open( '' , '_self' , '' );
        newWin.location = $( this ).attr('data-url');
    });

});