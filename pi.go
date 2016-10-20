package main

import "runtime"
import "time"
import "fmt"
import "os"
import "strconv"

var notify = make(chan int)
var result = make(chan float64)

func calc(id int, step float64, split int) {
    var x, pi float64
    base := id * split
    end := base + split

    <- notify
    fmt.Printf("%d start\n", id)

    for i := base; i < end; i++ {
        x = (float64(i) + 0.5) * step
        pi += 4 / (1 + x * x)
    }

    result <- pi
}

func main() {
    split, err := strconv.Atoi(os.Args[1])
    if err != nil {
        os.Exit(2)
    }
    num_thread := runtime.NumCPU()
    step := 1.0 / float64(split)
    thread_split := split / num_thread

    fmt.Printf("split: %d, step: %f, thread_split: %d\n", split, step, thread_split)

    start_t := time.Now()
    for i := 0; i < num_thread; i++ {
        go calc(i, step, thread_split)
        notify <- 0
    }

    var pi float64
    for i := 0; i < num_thread; i++ {
        pi += <-result
    }
    pi *= step
    elapsed := time.Since(start_t)

    fmt.Printf("pi: %f, time: %s\n", pi, elapsed)
}
