var listfields = function(record) {
    // list all fields as {key:key, value:value}..., generating one
    // such object for each field occurrence in repeating fields
    var result = [];
    var key, value;
    var tags = [];
    var non_tags = [];
    for (key in record) {
        if (key.match(/^v\d+$/)) {
            tags.push(parseInt(key.slice(1),10));
        } else {
            non_tags.push(key);
        }
    }
    tags.sort(function(a,b) { return a-b; });
    var idx = non_tags.concat(tags);
    for (var i=0; i<idx.length; i++) {
        key = (i < non_tags.length) ? idx[i] : 'v'+idx[i];
        value = record[key];
        if (Object.prototype.toString.call(value) === '[object Array]') {
            for (var j=0; j<value.length; j++) {
                result.push({key:key, value:value[j]});
            }
        } else {
            result.push({key:key, value:value});
        }
    }
    return result;
}

