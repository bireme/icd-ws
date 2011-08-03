========================================================
International Classification of Diseases - Web Services
========================================================

The goal of this project is to load ICD-10 data into CouchDB to create multi-lingual, developer-friendly, RESTful Web services.

-----------------
Record Structure
-----------------

Simple ''Subcategory'' type record:

  {
    code: "A07.3",
    lang: "pt-br",
    title: "Isosporíase",
    level: "subcat",
    inclusions: ["Coccidiose intestinal", "Infecção por Isospora belli e Isospora hominis", "Isosporíase"],
    seq: 108
  }


''Subcategory'' type record with inclusion notes and exclusion:

  { code: "A15.4",
    lang: "pt-br",
    title: "Tuberculose dos gânglios intratorácicos, com confirmação bacteriológica e histológica",
    level: "subcat",
    inclusions: ["Tuberculose ganglionar:", "- hilar", "- mediastinal", "- traqueobrônquica"],
    inc_notes: [{start:1, end:4,
                 col1: ["com confirmação bacteriológica", " e histológica"]}],
    exclusions ["Especificada como primária (A15.7)"],
    seq: 177
  }

"Pure" ''Category'' type record:

  { code: "T64",
    lang: "en",
    level: "cat",
    title: "Toxic effect of aflatoxin and other mycotoxin food contaminants"
  }

------------
Sample data
------------

For development and testing, a small subset of ICD-10 records will be selected including:

 * the first and last record of each chapter
 * the longest record (considering the number of attributes such as inclusions, exclusions, notes etc.)
 * all 6 records with two-column inclusion notes
 * at least one record with each of the following features:
  * multiple notes
  * notes with continuation (CNotes)
  * inclusion notes with one column
  * exclusion notes with one column
  * a star (*) mark on the cr_ast column
  * a cross (†) mark on the cr_ast column
  * chapter reference within a note
  * a code reference suffixed with a cross (†)
 * all records referenced from the records selected above

== Curly brackets Unicode characters ==

ICD-10 is annotated with curly brackets which can be built using the
following Unicode characters::

    007B    {   LEFT CURLY BRACKET
    007D    }   RIGHT CURLY BRACKET

    23A7    ⎧   LEFT CURLY BRACKET UPPER HOOK
    23A8    ⎨   LEFT CURLY BRACKET MIDDLE PIECE
    23A9    ⎩   LEFT CURLY BRACKET LOWER HOOK

    23AA    ⎪   CURLY BRACKET EXTENSION

    23AB    ⎫   RIGHT CURLY BRACKET UPPER HOOK
    23AC    ⎬   RIGHT CURLY BRACKET MIDDLE PIECE
    23AD    ⎭   RIGHT CURLY BRACKET LOWER HOOK

    23B0    ⎰   UPPER LEFT OR LOWER RIGHT CURLY BRACKET SECTION
    23B1    ⎱   UPPER RIGHT OR LOWER LEFT CURLY BRACKET SECTION

For example::

    23A7    ⎧   LEFT CURLY BRACKET UPPER HOOK
    23AA    ⎪   CURLY BRACKET EXTENSION
    23A8    ⎨   LEFT CURLY BRACKET MIDDLE PIECE
    23AA    ⎪   CURLY BRACKET EXTENSION
    23A9    ⎩   LEFT CURLY BRACKET LOWER HOOK









