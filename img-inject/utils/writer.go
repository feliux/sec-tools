package utils

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"

	"github.com/feliux/img-inject/types"
)

// WriteData writes new data to offset
func WriteData(bytesReader *bytes.Reader, c *types.CmdLineOpts, bytSlc []byte) {
	offset, err := strconv.ParseInt(c.Offset, 10, 64)
	if err != nil {
		log.Fatal(err)
	}

	file, err := os.OpenFile(c.Output, os.O_RDWR|os.O_CREATE, 0777)
	if err != nil {
		log.Fatal("Fatal: Problem writing to the output file...")
	}
	bytesReader.Seek(0, 0)

	var buff = make([]byte, offset)
	bytesReader.Read(buff)
	file.Write(buff)
	file.Write(bytSlc)
	if c.Decode {
		bytesReader.Seek(int64(len(bytSlc)), 1) // right bitshift to overwrite encode chunk
	}
	_, err = io.Copy(file, bytesReader)
	if err == nil {
		fmt.Printf("Success: %s created\n", c.Output)
	}
}
