
;; adds clozes around word before point
(defun cloze-word ()
  (interactive)
  
  (cond
  ( (not (= (char-before (point)) ? ))
    (backward-word 1))
  )
 
 (insert (concat "{c1::"))
 (forward-word 1)
 (insert "}}")
 )

(define-key text-mode-map "\C-cc" 'cloze-word)

;; creates a deck using the anki.py file
(defun make-deck ()
  (interactive)
  (message (shell-command-to-string "makeanki"))
  )

(define-key text-mode-map "\C-cd" 'make-deck)
