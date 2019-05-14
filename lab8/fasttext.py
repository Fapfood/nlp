import fastText

classifier = fastText.train_supervised('train-100%.txt')
# classifier.save_model('model-100%')
result = classifier.test_label('test-100%.txt')
print(result)

classifier = fastText.train_supervised('train-10%.txt')
# classifier.save_model('model-10%')
result = classifier.test_label('test-10%.txt')
print(result)

classifier = fastText.train_supervised('train-10.txt')
# classifier.save_model('model-10')
result = classifier.test_label('test-10.txt')
print(result)

classifier = fastText.train_supervised('train-1.txt')
# classifier.save_model('model-1')
result = classifier.test_label('test-1.txt')
print(result)
