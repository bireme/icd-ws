function(doc) {
  if (doc.code) {
    emit(doc.code, doc.title);
  }
};
