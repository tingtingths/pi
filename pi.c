#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_size, rank;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    long long split, base, roof;
    long double step, psplit, result, global_result;

    // parse argv
    if (rank == 0) {
        if (argc >= 2) {
            sscanf(argv[1], "%i", &split);
        } else {
            split = 900000000;
        }
    }
    MPI_Bcast(&split, 1, MPI_LONG_LONG, 0, MPI_COMM_WORLD);

    step = 1.0 / split;
    psplit = split / world_size;

    base = (int) rank * psplit;
    roof = (int) base + psplit;

    if (rank == 0) {
        printf("world_size: %d, split: %lld, step: %Lg\n", world_size, split, step);
    }

    double t_start, t_end;
    if (rank == 0) {
        t_start = MPI_Wtime();
    }

    for (long long i = base; i < roof; i++) {
        long double x = (i + 0.5) * step;
        result = result + 4.0 / (1.0 + x * x);
    }

    MPI_Reduce(&result, &global_result, 1, MPI_LONG_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        t_end = MPI_Wtime();
        global_result *= step;
        printf("Pi: %.30Lg\n", global_result);
        printf("Elapsed: %.6fs\n", t_end - t_start);
    }

    MPI_Finalize();
}
