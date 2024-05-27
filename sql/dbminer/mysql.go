package dbminer

import (
	"database/sql"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

type MySQLMiner struct {
	Url string
	Db  sql.DB
}

func New(url string) (*MySQLMiner, error) {
	m := MySQLMiner{Url: url}
	err := m.connect(url)
	if err != nil {
		return nil, err
	}
	return &m, nil
}

func (m *MySQLMiner) connect(url string) error {
	db, err := sql.Open("mysql", url)
	if err != nil {
		log.Panicln(err)
	}
	m.Db = *db
	return nil
}

func (m *MySQLMiner) GetSchema() (*Schema, error) {
	var s = new(Schema)
	sql := `SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME FROM columns
	WHERE TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
	ORDER BY TABLE_SCHEMA, TABLE_NAME`
	schemarows, err := m.Db.Query(sql)
	if err != nil {
		return nil, err
	}
	defer schemarows.Close()

	var prevschema, prevtable string
	var db Database
	var table Table
	for schemarows.Next() {
		var currschema, currtable, currcol string
		if err := schemarows.Scan(&currschema, &currtable, &currcol); err != nil {
			return nil, err
		}

		if currschema != prevschema {
			if prevschema != "" {
				db.Tables = append(db.Tables, table)
				s.Databases = append(s.Databases, db)
			}
			db = Database{Name: currschema, Tables: []Table{}}
			prevschema = currschema
			prevtable = ""
		}

		if currtable != prevtable {
			if prevtable != "" {
				db.Tables = append(db.Tables, table)
			}
			table = Table{Name: currtable, Columns: []string{}}
			prevtable = currtable
		}
		table.Columns = append(table.Columns, currcol)
	}
	db.Tables = append(db.Tables, table)
	s.Databases = append(s.Databases, db)
	if err := schemarows.Err(); err != nil {
		return nil, err
	}
	return s, nil
}
