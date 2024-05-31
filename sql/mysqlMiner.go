package main

import (
	"fmt"
	"os"

	"github.com/feliux/sql/dbminer"
)

func main() {
	host := os.Args[1]
	url := fmt.Sprintf("admin:changeme@tcp(%s:3306)/information_schema", host)
	mysqlMiner, err := dbminer.New(url)
	if err != nil {
		panic(err)
	}
	defer mysqlMiner.Db.Close()
	if err := dbminer.Search(mysqlMiner); err != nil {
		panic(err)
	}
}
