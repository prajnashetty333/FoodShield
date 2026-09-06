import axios from 'axios';
import {
  OverviewResponse,
  CountryOptions,
  CountryAnalysisResponse,
  CommodityAnalysisResponse,
  ShockAnalysisResponse,
  ReplacementAnalysisResponse,
  SensitivityAnalysisResponse,
  PolicyResponse,
  MethodologyResponse
} from '../types';

const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, ''),
});

export const fetchOverview = async (): Promise<OverviewResponse> => {
  const { data } = await api.get('/overview');
  return data;
};

export const fetchCountryOptions = async (): Promise<CountryOptions> => {
  const { data } = await api.get('/countries/options');
  return data;
};

export const fetchCountryAnalysis = async (country: string, commodity: string, year: number): Promise<CountryAnalysisResponse> => {
  const { data } = await api.get('/countries/analysis', {
    params: { country, commodity, year }
  });
  return data;
};

export const fetchCommodities = async (): Promise<string[]> => {
  const { data } = await api.get('/commodities');
  return data;
};

export const fetchCommodityAnalysis = async (commodity: string): Promise<CommodityAnalysisResponse> => {
  const { data } = await api.get('/commodities/analysis', {
    params: { commodity }
  });
  return data;
};

export const fetchShockAnalysis = async (country: string, commodity: string, year: number, rank: number): Promise<ShockAnalysisResponse> => {
  const { data } = await api.get('/shocks/analysis', {
    params: { country, commodity, year, rank }
  });
  return data;
};

export const fetchReplacementAnalysis = async (country: string, commodity: string, year: number, rank: number): Promise<ReplacementAnalysisResponse> => {
  const { data } = await api.get('/replacement/analysis', {
    params: { country, commodity, year, rank }
  });
  return data;
};

export const fetchSensitivity = async (): Promise<SensitivityAnalysisResponse> => {
  const { data } = await api.get('/sensitivity/analysis');
  return data;
};

export const fetchPolicy = async (): Promise<PolicyResponse> => {
  const { data } = await api.get('/policy');
  return data;
};

export const fetchMethodology = async (): Promise<MethodologyResponse> => {
  const { data } = await api.get('/methodology');
  return data;
};
