;;;; -*-  Mode: LISP; Syntax: Common-Lisp; Base: 10                          -*-
;;;; ---------------------------------------------------------------------------
;;;; File name: pythonian_lisp_helpers.lsp
;;;;    System: Companions
;;;;    Author: Blass
;;;;   Created: May 31, 2017 15:24:01
;;;;   Purpose: 
;;;; ---------------------------------------------------------------------------
;;;;  $LastChangedDate: 2017-06-29 14:58:20 -0500 (Thu, 29 Jun 2017) $
;;;;  $LastChangedBy: blass $
;;;; ---------------------------------------------------------------------------

(in-package :cl-user)

;;; this is a place to put lisp helper functions for all your pythonian needs

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun savePythonianImageResults () ;; need a list of file names IN QUOTES, unfortunately - how to get this?
  (let* ((*print-right-margin* 1000000000000000000))
    (with-open-file (str (make-qrg-file-name (make-qrg-path "companions" "v1" "pythonian") "image_data.csv") :direction :output :if-exists :supersede)
      (format str "fileName,label,facts~%")
      (dolist (filepath (directory "/qrg/companions/v1/pythonian/labelimg/images/*.jpg"))
        (let* ((string (namestring filepath))
               (split (split-re "\\\\" string))
               (namepg (last split))
               (splitname (split-re "[.]" (car namepg)))
               (name (car splitname))
               (label (car (fire::ask-it `(ist-Information (labelOfImage ,name) (imageLabel ,name ?label)) :response '?label)))
               (facts (fire::ask-it `(ist-Information (labelOfImage ,name) ?fact) :response '?fact))
               (clean-facts (remove `(imageLabel ,name ,label) facts)))
          (format str "~A,~A,~A~%" name label clean-facts))))))
  

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; End of Code