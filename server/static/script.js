function template(data){
    let html = "<div id='flats'>";
    $.each(data, function(index, item){
        html += "<div class='flat'>" +
            "<img class='flat-img' src='" + item.image_url + "'/><div class='flat-title'>" + item.title + "</div>" +
            "</div>";
    })
    html += "</div>";
    return html;
}

window.onload = function () {
    fetch('/api/flats')
        .then(response => response.json())
        .then(data => {
            $('#pagination-container').pagination({
                dataSource: data,
                pageSize: 10,
                locator: function () {return 'result'},
                callback: function(d, pagination) {
                    let html = template(d);
                    $('#data-container').html(html);
                }
            })
        })
        .catch(error => {
            console.log(error);
        });
};
