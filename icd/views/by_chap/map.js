function(doc) {
  if(doc.level == 'chap'){
    emit(doc.chap, doc.title + ' [' + doc._id + ']');
  }
}
