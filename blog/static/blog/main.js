function writeArchive() {
    $.get('/blog/api/archive/', function(data, status){
        var a_ul = $('<ul class="w3-ul"></ul>');
        for (var i in data) {
            var li = $('<li></li>');
            var b_ul = $('<ul class="w3-ul w3-border-purple w3-leftbar ar_for_'+i+'"></ul>');
            li.append(
                "<span class=\"w3-large w3-button\" style=\"padding:2px\" onclick=\"$('.ar_for_"+i+"').slideToggle()\">"+i+"</span>"
            );
            li.append(b_ul);
            for (var e in data[i]) {
                var b_li = $('<li></li>');
                var c_ul = $('<ul class="w3-ul w3-border-purple w3-leftbar list_for_'+e+'_'+i+'"><ul>');
                b_li.prepend(c_ul);
                b_li.prepend(
                    '<span class="w3-large w3-button" style="padding:2px" onclick="$(\'.list_for_'+e+'_'+i+'\').slideToggle()">'+e+'</span>'
                );
                b_ul.append(b_li);
                for (var m = 0; m < data[i][e].length; m++) {
                    c_ul.append(
                        '<li><a href="/blog/detail/'+ data[i][e][m][0] +'" class="w3-hover-blue" style="text-decoration:none"><span class="w3-large">('+data[i][e][m][1]+')</span> '+ data[i][e][m][2] +'</a></li>'
                    );
                }
            }
            a_ul.prepend(li);
        }
        $('.writeArchiveHere').html(a_ul);
    });
}

$(document).ready(function(){
    $('#archive').css('height', $('#articles').css('height'));
    writeArchive();
});