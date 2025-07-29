#!/usr/bin/env bash

uv run  glyphsieve pipeline --input ./glyphsieve/demo/input.csv --output ./glyphsieve/demo/output.csv --quantize-capacity --working-dir ./glyphsieve/demo/intermediate >  glyphsieve/demo/stdout.txt
