import pytest
import PyStoAnalyzer.pattern_tool as tool
from transformers import pipeline
# pattern = tool.DisplayPattern.load_patterns()
# print(patternfrom transformers import pipeline


pipe = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
print(pipe("hello are working fine"))
