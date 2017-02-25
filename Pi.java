import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Pi {

    public static void main(String[] args) {
        long split = Long.parseLong(args[0]);
        double sum = new Pi(1.0/split, 0, split).calc();
        System.out.println("Pi : " + (sum * (1.0 / split)));
    }

    private double step;
    private long floor;
    private long ceil;
    private double result;

    public Pi(double step, long floor, long ceil) {
        this.step = step;
        this.floor = floor;
        this.ceil = ceil;
    }

    public double calc() {
        long startTime = System.nanoTime();
        long endTime;

        // multithreading
        int processors = Runtime.getRuntime().availableProcessors();
        System.out.println("Processors: " + processors);
        ExecutorService executor = Executors.newFixedThreadPool(processors);
        long threadSplit = (ceil - floor) / processors;
        for (int i = 0; i < processors; i++) {
            long floor = (i * threadSplit) + this.floor;
            long ceil = floor + threadSplit;
            executor.submit(() -> {
                threadCalc(floor, ceil);
            });
        }
        // wait all threads
        executor.shutdown();
        try {
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        endTime = System.nanoTime();
        double escaped = (endTime - startTime) / 1000000000.0;
        System.out.println("Calculation time: " + escaped + " second(s)");

        return result;
    }

    private void threadCalc(long floor, long ceil) {
        double x;
        double result = 0.0;

        for (long i = floor; i < ceil; i++) {
            x = (i + 0.5) * step;
            result = result + 4 / (1 + x * x);
        }

        // add result, one thread only
        addResult(result);
    }

    private synchronized void addResult(double d) {
        result += d;
    }
}
