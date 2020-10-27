function setCurTime(time) {
    audio.currentTime = time;
}

// Get Current Time automatically through html audio control player
function getCurTime() {
    currentTime = audio.currentTime;
    var allTimeTags = document.querySelectorAll(['a.startTime', 'a.endTime']);
    var allParagraphTags = document.getElementsByClassName('transcription_paragraph');
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
                    // Clean up everything as white before highlighting again
                    $(".highlight").css("background-color", "#ffffff");          
                    // Highlight in orange                       
                    document.getElementById(highlight_id).style.backgroundColor = "#ffdfa3";            
                }
            }
        }
   }
}

function previousPage(internalMeetingId) {
    var meetingPresentationDoc = document.getElementById("meetingPresentation");
    var dataAttr = meetingPresentationDoc.data;
    var newArray = dataAttr.split('/');
    var lastElement = newArray.slice(-1)[0];
    var slideString = lastElement.split('.')[0];
    var slideNumberString = slideString.replace( /^\D+/g, '');            // cut out all string but the number
    var slideNumber = parseInt(slideNumberString);
    if (slideNumber == 1) {
        return true;
    } else {
        var previousSlideNumber = (slideNumber - 1).toString();
        var newData = "/summarize/static/img/" + internalMeetingId + "/slide" + previousSlideNumber + ".svg";
        document.getElementById("meetingPresentation").setAttribute('data', newData);
    }
}

function nextPage(internalMeetingId) {
    var meetingPresentationDoc = document.getElementById("meetingPresentation");
    var dataAttr = meetingPresentationDoc.data;
    var newArray = dataAttr.split('/');
    var lastElement = newArray.slice(-1)[0];
    var slideString = lastElement.split('.')[0];
    var slideNumberString = slideString.replace( /^\D+/g, '');            // cut out all string but the number
    var slideNumber = parseInt(slideNumberString);
    var previousSlideNumber = (slideNumber + 1).toString();
    var newData = "/summarize/static/img/" + internalMeetingId + "/slide" + previousSlideNumber + ".svg";
    document.getElementById("meetingPresentation").setAttribute('data', newData);
}

// used if audio or transcription is triggered
function jumpToPage(pageNumber) {
    var newData = "/summarize/static/img/" + internalMeetingId + "/slide" + pageNumber + ".svg";
    document.getElementById("meetingPresentation").setAttribute('data', newData);
}