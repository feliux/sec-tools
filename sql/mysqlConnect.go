package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

const (
	uri   string = "admin:changeme@tcp(127.0.0.1:3306)/myddbb"
	query string = "SELECT ccnum, date, amount, cvv, exp FROM transactions"
)

var (
	ccnum, date, cvv, exp string
	amount                float32
)

func main() {
	db, err := sql.Open("mysql", uri)
	if err != nil {
		log.Panicln(err)
	}
	defer db.Close()
	rows, err := db.Query(query)
	if err != nil {
		log.Panicln(err)
	}
	defer rows.Close()
	for rows.Next() {
		err := rows.Scan(&ccnum, &date, &amount, &cvv, &exp)
		if err != nil {
			log.Panicln(err)
		}
		fmt.Println(ccnum, date, amount, cvv, exp)
	}
	if rows.Err() != nil {
		log.Panicln(err)
	}
}
