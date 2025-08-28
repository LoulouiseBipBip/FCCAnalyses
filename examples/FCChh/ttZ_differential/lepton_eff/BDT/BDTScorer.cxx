
#include <xgboost/c_api.h>
#include <ROOT/RVec.hxx>
#include <stdexcept>
#include <iostream>
#include <mutex>
#include <unordered_map>
#include <cmath>

using RVecF = ROOT::VecOps::RVec<float>;

// Global model cache to avoid reloading models per event
static std::unordered_map<std::string, BoosterHandle> model_cache;
static std::mutex model_cache_mutex;

RVecF computeBDTScores(
    RVecF d0, RVecF z0,
    RVecF iso1, RVecF iso2, RVecF iso3, RVecF iso4,
    RVecF pt, RVecF eta, const char* modelPath) {
    // Check input sizes
    size_t n_entries = d0.size();
    //std::cout << "computeBDTScores called with n_entries=" << n_entries << std::endl;
    if (n_entries != z0.size() || n_entries != iso1.size() || n_entries != iso2.size() ||
        n_entries != iso3.size() || n_entries != iso4.size() || n_entries != pt.size() ||
        n_entries != eta.size()) {
        std::cerr << "Error: Input RVecs have mismatched sizes: "
                  << "d0=" << d0.size() << ", z0=" << z0.size()
                  << ", iso1=" << iso1.size() << ", iso2=" << iso2.size()
                  << ", iso3=" << iso3.size() << ", iso4=" << iso4.size()
                  << ", pt=" << pt.size() << ", eta=" << eta.size() << std::endl;
        throw std::runtime_error("Input RVecs have mismatched sizes");
    }

    // Log all input values
    for (size_t i = 0; i < n_entries; ++i) {
        //std::cout << "Entry " << i << ": d0=" << d0[i] << ", z0=" << z0[i]
        //                  << ", iso1=" << iso1[i] << ", iso2=" << iso2[i]
        //                  << ", iso3=" << iso3[i] << ", iso4=" << iso4[i]
        //                  << ", pt=" << pt[i] << ", eta=" << eta[i] << std::endl;
        // Check for NaN or infinity
        if (std::isnan(d0[i]) || std::isinf(d0[i]) ||
            std::isnan(z0[i]) || std::isinf(z0[i]) ||
            std::isnan(iso1[i]) || std::isinf(iso1[i]) ||
            std::isnan(iso2[i]) || std::isinf(iso2[i]) ||
            std::isnan(iso3[i]) || std::isinf(iso3[i]) ||
            std::isnan(iso4[i]) || std::isinf(iso4[i]) ||
            std::isnan(pt[i]) || std::isinf(pt[i]) ||
            std::isnan(eta[i]) || std::isinf(eta[i])) {
            std::cerr << "Error: NaN or Inf detected in entry " << i << std::endl;
            throw std::runtime_error("NaN or Inf in input data");
        }
    }

    // Load or retrieve model from cache
    BoosterHandle booster = nullptr;
    std::string model_path_str(modelPath);
    {
        std::lock_guard<std::mutex> lock(model_cache_mutex);
        auto it = model_cache.find(model_path_str);
        if (it == model_cache.end()) {
            //std::cout << "Loading model from: " << modelPath << std::endl;
            if (XGBoosterCreate(nullptr, 0, &booster) != 0) {
                throw std::runtime_error("Failed to create XGBoost booster");
            }
            if (XGBoosterLoadModel(booster, modelPath) != 0) {
                std::cerr << "Error: Failed to load XGBoost model from " << modelPath << std::endl;
                XGBoosterFree(booster);
                throw std::runtime_error("Failed to load XGBoost model from " + model_path_str);
            }
            model_cache[model_path_str] = booster;
        } else {
            booster = it->second;
            //std::cout << "Using cached model for: " << modelPath << std::endl;
        }
    }

    // Prepare input data
    RVecF scores(n_entries);
    for (size_t i = 0; i < n_entries; ++i) {
        //std::cout << "Processing entry " << i << std::endl;
        float data[8] = {d0[i], z0[i], iso1[i], iso2[i], iso3[i], iso4[i], pt[i], eta[i]};
        DMatrixHandle dmatrix;
        //std::cout << "Creating DMatrix for entry " << i << std::endl;
        if (XGDMatrixCreateFromMat(data, 1, 8, -999, &dmatrix) != 0) {
            throw std::runtime_error("Failed to create XGBoost DMatrix for entry " + std::to_string(i));
        }

        //std::cout << "Calling XGBoosterPredict for entry " << i << std::endl;
        const float* out_result;
        bst_ulong out_len;
        if (XGBoosterPredict(booster, dmatrix, 0, 0, 0, &out_len, &out_result) != 0) {
            XGDMatrixFree(dmatrix);
            throw std::runtime_error("Failed to compute XGBoost prediction for entry " + std::to_string(i));
        }
        if (out_len != 1) {
            XGDMatrixFree(dmatrix);
            throw std::runtime_error("Unexpected prediction output length: " + std::to_string(out_len) + " for entry " + std::to_string(i));
        }
        scores[i] = out_result[0];
        //std::cout << "Score for entry " << i << ": " << scores[i] << std::endl;
        XGDMatrixFree(dmatrix);
    }

    return scores;
}
