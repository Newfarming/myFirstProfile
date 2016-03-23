function back_button(){
    window.history.go(-1);
};

$(function(){
    function get_undo(){
        $.get("/crm/calendar/undo/", function(e){
            $("#undo_count").html(e.all_count);
            $("#all_count").html(e.all_count);
            $("#alarm_count").html(e.alarm_count);
            $("#custom_schedule_count").html(e.custom_schedule_count);
        });
    }
get_undo();
setInterval(get_undo,150000);
});
