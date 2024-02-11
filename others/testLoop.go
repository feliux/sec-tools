package main

import (
	"fmt"
	//"sync"
)

const limit int = 1048575 // panic: too many concurrent operations on a single file or socket (max 1048575)
/*
// 0m7,442s
func main() {
	var wg sync.WaitGroup
	wg.Add(limit)
	for i := 0; i < limit; i++ {
		go func(i int, wg *sync.WaitGroup){
			defer wg.Done()
			fmt.Println(i)
		}(i, &wg)
	}
	wg.Wait()
}
*/

// 0m4,252s
func main() {
	c := make(chan int, 10)
	for i := 0; i < limit; i++ {
		go func(i int, c chan int) {
			fmt.Println(i)
			c <- i
		}(i, c)
	}
	<-c
}

/*
// 0m4,140s
func main() {
	for i := 0; i < limit; i++ {
		fmt.Println(i)
	}
}
*/
