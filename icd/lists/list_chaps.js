function(head, req) {
    var ddoc = this;
    var Mustache = require("vendor/couchapp/lib/mustache");
    var head_list = [];
    var row;
    var rows = [];
    start({
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        }
    });
    
    for (k in head) {
	    head_list.push({'key':k, 'value':head[k]});
    }
    
    while(row = getRow()){
        rows.push({'chap':row.key,
                   'title':row.value});
    }
    rows.sort();
    var view = {
        head: head_list,
        rows: rows,
        json_url: '/cid10/_design/icd/_view/by_chap'
    }
    
    var html = Mustache.to_html(ddoc.templates.list, view);
    send(html);
        
  
}
