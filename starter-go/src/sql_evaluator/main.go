package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path"

	"sql_evaluator/sqleval"
)

func usageString() string {
	return fmt.Sprintf("Usage: %s <table-folder> <sql-json-file> <output-file>\n", os.Args[0])
}

func die(message string) {
	os.Stderr.WriteString(message)
	os.Exit(1)
}

func main() {
	if len(os.Args) != 4 {
		die(usageString())
	}

	tableFolder := os.Args[1]
	sqlJsonFile := os.Args[2]
	outputFile := os.Args[3]

	var query sqleval.Query
	{
		err := jsonUnmarshalFromFile(sqlJsonFile, &query)
		if err != nil {
			die(fmt.Sprintf("Error reading %q: %s\n", sqlJsonFile, err))
		}
	}

	var tables []sqleval.Table = nil
	for _, tableDecl := range query.From {
		tableJsonFile := path.Join(tableFolder, tableDecl.Source+".table.json")
		var table sqleval.Table
		err := jsonUnmarshalFromFile(tableJsonFile, &table)
		if err != nil {
			die(fmt.Sprintf("Error reading %q: %s\n", tableJsonFile, err))
		}
		tables = append(tables, table)
	}

	// TODO: Actually evaluate query.
	// For now, just dump the input back out.
	{
		fw, err := os.Create(outputFile)
		if err != nil {
			die(fmt.Sprintf("Error opening %q for writing: %s\n", outputFile, err))
		}
		defer fw.Close()

		w := bufio.NewWriter(fw)
		defer w.Flush()

		mustJsonMarshalIndent(w, query)

		for _, table := range tables {
			w.WriteString("[\n")

			w.WriteString("    ")
			mustJsonMarshal(w, table.Columns)

			for _, row := range table.Rows {
				w.WriteString(",\n    ")
				mustJsonMarshal(w, row)
			}

			w.WriteString("\n]\n")
		}
	}
}

// NOTE: Not using json.Decoder because it doesn't error if there's trailing garbage.
func jsonUnmarshalFromFile(path string, v interface{}) error {
	contents, err := ioutil.ReadFile(path)
	if err != nil {
		return err
	}
	return json.Unmarshal(contents, v)
}

func newJsonEncoder(w io.Writer) *json.Encoder {
	encoder := json.NewEncoder(w)
	// By default, "&", "<", and ">" are escaped, which makes the output harder to read.  Disable that.
	encoder.SetEscapeHTML(false)
	return encoder
}

func mustJsonMarshal(w io.Writer, v interface{}) {
	buffer := &bytes.Buffer{}
	encoder := newJsonEncoder(buffer)
	err := encoder.Encode(v)
	if err != nil {
		panic(fmt.Sprintf("Can't happen: value should remarshal, but got error: %v", err))
	}
	// Ugh, Encode() adds a newline even though Marshal() does not.  Remove it.
	raw := buffer.Bytes()
	end := len(raw) - 1
	if raw[end] != '\n' {
		panic("Last byte written by Encode() wasn't a newline.")
	}
	raw = raw[:end]
	w.Write(raw)
}

func mustJsonMarshalIndent(w io.Writer, v interface{}) {
	encoder := newJsonEncoder(w)
	encoder.SetIndent("", "    ")
	err := encoder.Encode(v)
	if err != nil {
		panic(fmt.Sprintf("Can't happen: value should remarshal, but got error: %v", err))
	}
}
