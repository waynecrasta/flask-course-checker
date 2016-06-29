            $(document).ready(function() {
                $.getJSON("/static/js/lol.json",function(obj) {
                    var $department = $("#department");
                    var $course = $("#course");
                    var $crn = $("#crn")

                    $department.chosen({width:"10%",placeholder_text_single: "Choose"});
                    $course.chosen({width: "5%", placeholder_text_single: "101"});
                    $crn.chosen({width:"6%", placeholder_text_single: "30109"});

                    $department.append("<option disabled selected>Choose</option>");
                    $.each(obj,function(key,value) {
                        $department.append("<option>" + key + "</option>");
                    });
                    $department.trigger("chosen:updated");
                    
                    $department.chosen().change(function() {
                        $course.empty()
                        var numberdict = obj[$department.chosen().val()]
                        $.each(numberdict,function(key,value) {
                            $course.append("<option>" + key + "</option>");
                        });
                        $course.trigger("chosen:updated");
                    });
                    $course.change(function() {
                        $crn.empty()
                        var crndict = obj[$department.chosen().val()][$course.chosen().val()];
                        $.each(crndict,function(key,value) {
                            $crn.append("<option>" + value + "</option>");
                        });
                        $crn.trigger("chosen:updated");
                    });
                });
            });
