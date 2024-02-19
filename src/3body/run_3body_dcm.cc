/**
 * Main file for running the 3-body DCM within the dcEmb package
 *
 * Copyright (C) 2022 Embecosm Limited
 *
 * Contributor William Jones <william.jones@embecosm.com>
 * Contributor Elliot Stein <E.Stein@soton.ac.uk>
 *
 * This file is part of the dcEmb package
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <DEM_3body.hh>
#include <Eigen/Eigen>
#include <iostream>
#include <run_3body_dcm.hh>

/**
 * Check number of threads Eigen is operating on, then run 3body test
 */
int main(int argc, char *argv[]) {
  if (argc != 2) {
    std::cerr << "Usage: " << argv[0] << " <noise>\n";
    return 1;
  }
#if defined(_OPENMP)
  std::cout << "OpenMP multithreading enabled with " << Eigen::nbThreads()
            << " cores" << '\n';
#else
  std::cout << "OpenMP multithreading not enabled, using " << Eigen::nbThreads()
            << " cores" << '\n';
#endif
  int test = run_3body_test(argv[1], atof(argv[1]));
  return (0);
}
