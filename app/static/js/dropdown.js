$(document).ready(function() {
    new Clipboard('.btn');
    $.getJSON("/static/js/data.json",function(obj) {
        var $department = $("#department");
        var $course = $("#course");
        var $crn = $("#crn")

        $department.chosen({width:"10%",placeholder_text_single: "Choose"});
        $course.chosen({width: "10%", placeholder_text_single: "Choose"});
        $crn.chosen({width:"10%", placeholder_text_single: "Choose"});

        $department.append("<option disabled selected>Choose</option>");
        $.each(obj,function(key,value) {
            $department.append("<option>" + key + "</option>");
        });
        $department.trigger("chosen:updated");
        
        $department.chosen().change(function() {
            $course.empty()
            var numberdict = obj[$department.chosen().val()]
            $course.append("<option disabled selected>Choose</option>");
            $.each(numberdict,function(key,value) {
                $course.append("<option>" + key + "</option>");
            });
            $course.trigger("chosen:updated");
        });
        $course.change(function() {
            $crn.empty()
            var crndict = obj[$department.chosen().val()][$course.chosen().val()];
            $crn.append("<option disabled selected>Choose</option>");
            $.each(crndict,function(key,value) {
                $crn.append("<option>" + value + "</option>");
            });
            $crn.trigger("chosen:updated");
        });
    });
});
