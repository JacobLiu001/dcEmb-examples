/**
 * The 3-body dynamic causal model class within the dcEmb package
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

#include "Eigen/Dense"
#include "parameter_location_3body.hh"
#pragma once

int run_3body_test(std::string x_string, double x);

Eigen::VectorXd true_prior_expectations();
Eigen::VectorXd default_prior_expectations(double x);
Eigen::MatrixXd default_prior_covariances();
parameter_location_3body default_parameter_locations();
Eigen::VectorXd default_hyper_expectations();
Eigen::MatrixXd default_hyper_covariances();
