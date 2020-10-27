function setCurTime(time) {
    audio.currentTime = time;
}

function getCurTime() {
    currentTime = audio.currentTime;
    var allTimeTags = document.querySelectorAll(['a.startTime', 'a.endTime']);
    // var allParagraphTags = document.getElementsByTagName('p');
    var allParagraphTags = document.getElementsByClassName('transcription_paragraph');
    // see which currentTime is between startTime and endTime
    for (var i=0; i < allTimeTags.length; i++) {
        var test = i % 2;
        // Dom structure is: startTime, endTime, startTime, endTime, ...
        if (test == 0) {
            var startTime = parseInt(allTimeTags[i].innerHTML);
        } else {
            var endTime = parseInt(allTimeTags[i].innerHTML);
        }
        // highlight the span which is the nextSiblingElement of endTime
        if (startTime < currentTime && currentTime < endTime) {
            var correct_endTime = allTimeTags[i].innerHTML;
            // iterate through to search for endtime == correct_endTime
            for (var j=0; j < allParagraphTags.length; j++) {
                var stringTime = allParagraphTags[j].nextElementSibling.children[1].innerHTML;
                if (correct_endTime == stringTime) {
                    var highlight_id = allParagraphTags[j].nextElementSibling.nextElementSibling.children[0].id;
                    $(".highlight").css("background-color", "#ffffff");                                 // white
                    document.getElementById(highlight_id).style.backgroundColor = "#ffdfa3";            // orange
                }
            }
        }
   }
}


