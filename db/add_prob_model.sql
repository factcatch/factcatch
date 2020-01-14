ALTER TABLE claim
ADD COLUMN prob_model FLOAT;
UPDATE claim SET prob_model=random();