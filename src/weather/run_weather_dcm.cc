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

#include <DEM_weather.hh>
#include <Eigen/Eigen>
#include <iostream>
#include <fstream>
#include <run_weather_dcm.hh>

/**
 * Check number of threads Eigen is operating on, then run weather test
 */
int main(int argc, char *argv[]) {
  if (argc != 3) {
    std::cerr << "Usage: " << argv[0] << " <scenario> <true_prior_expectations_filename>" << '\n';
    std::cerr << "Where <true_prior_expectations_filename> contains 11 space-separated numbers." << '\n';
    exit(1);
  }
  std::string scenario = argv[1];
  std::string true_prior_expectations_filename = argv[2];

  std::ifstream true_prior_expectations_file(true_prior_expectations_filename);
  if (!true_prior_expectations_file.is_open()) {
    std::cerr << "Error: could not open file " << true_prior_expectations_filename << '\n';
    exit(1);
  }
  std::vector<double> true_prior_expectations;

  for (int i = 0; i < 11; i++) {
    double expectation;
    true_prior_expectations_file >> expectation;
    true_prior_expectations.push_back(expectation);
  }
#if defined(_OPENMP)
  std::cout << "OpenMP multithreading enabled with " << Eigen::nbThreads()
            << " cores" << '\n';
#else
  std::cout << "OpenMP multithreading not enabled, using " << Eigen::nbThreads()
            << " cores" << '\n';
#endif
  int test = run_weather_test(scenario, true_prior_expectations);
  return 0;
}
