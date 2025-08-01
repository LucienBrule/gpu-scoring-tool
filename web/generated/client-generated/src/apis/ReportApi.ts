/* tslint:disable */
/* eslint-disable */
/**
 * Glyphd: GPU Market API
 * API service exposing enriched GPU listingsmodel metadata, scoring reports, and insight overlays from the glyphsieve pipeline.
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  ReportDTO,
} from '../models/index';
import {
    ReportDTOFromJSON,
    ReportDTOToJSON,
} from '../models/index';

/**
 * 
 */
export class ReportApi extends runtime.BaseAPI {

    /**
     * Retrieve the latest GPU market insight report with summary statistics and scoring weights
     * Get Market Insight Report
     */
    async getReportApiReportGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<ReportDTO>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};


        let urlPath = `/api/report`;

        const response = await this.request({
            path: urlPath,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => ReportDTOFromJSON(jsonValue));
    }

    /**
     * Retrieve the latest GPU market insight report with summary statistics and scoring weights
     * Get Market Insight Report
     */
    async getReportApiReportGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<ReportDTO> {
        const response = await this.getReportApiReportGetRaw(initOverrides);
        return await response.value();
    }

}
