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

import { mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface HealthStatus
 */
export interface HealthStatus {
    /**
     * 
     * @type {string}
     * @memberof HealthStatus
     */
    status: string;
}

/**
 * Check if a given object implements the HealthStatus interface.
 */
export function instanceOfHealthStatus(value: object): value is HealthStatus {
    if (!('status' in value) || value['status'] === undefined) return false;
    return true;
}

export function HealthStatusFromJSON(json: any): HealthStatus {
    return HealthStatusFromJSONTyped(json, false);
}

export function HealthStatusFromJSONTyped(json: any, ignoreDiscriminator: boolean): HealthStatus {
    if (json == null) {
        return json;
    }
    return {
        
        'status': json['status'],
    };
}

export function HealthStatusToJSON(json: any): HealthStatus {
    return HealthStatusToJSONTyped(json, false);
}

export function HealthStatusToJSONTyped(value?: HealthStatus | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'status': value['status'],
    };
}

