import { apiService } from './apiService';

export interface Company {
  id: string;
  name: string;
  description?: string;
  contact_email: string;
  contact_phone?: string;
  address?: string;
  operation_area_type: 'circle' | 'polygon';
  center_lat?: number;
  center_lng?: number;
  radius_km?: number;
  polygon_coordinates?: Array<{ lat: number; lng: number }>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  driver_count: number;
  drivers?: Driver[];
}

export interface Driver {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  is_active: boolean;
}

export interface CompanyCreate {
  name: string;
  description?: string;
  contact_email: string;
  contact_phone?: string;
  address?: string;
  operation_area_type: 'circle' | 'polygon';
  center_lat?: number;
  center_lng?: number;
  radius_km?: number;
  polygon_coordinates?: Array<{ lat: number; lng: number }>;
  is_active?: boolean;
}

export interface CompanyUpdate {
  name?: string;
  description?: string;
  contact_email?: string;
  contact_phone?: string;
  address?: string;
  operation_area_type?: 'circle' | 'polygon';
  center_lat?: number;
  center_lng?: number;
  radius_km?: number;
  polygon_coordinates?: Array<{ lat: number; lng: number }>;
  is_active?: boolean;
}

class CompanyService {
  private baseUrl = '/api/companies/';

  async getCompanies(params?: {
    skip?: number;
    limit?: number;
    search?: string;
    is_active?: boolean;
  }): Promise<Company[]> {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.is_active !== undefined) queryParams.append('is_active', params.is_active.toString());

    const url = `${this.baseUrl}?${queryParams.toString()}`;
    return apiService.request<Company[]>(url);
  }

  async getCompany(id: string): Promise<Company> {
    return apiService.request<Company>(`${this.baseUrl}${id}/`);
  }

  async createCompany(companyData: CompanyCreate): Promise<Company> {
    return apiService.request<Company>(this.baseUrl, {
      method: 'POST',
      body: JSON.stringify(companyData)
    });
  }

  async updateCompany(id: string, companyData: CompanyUpdate): Promise<Company> {
    return apiService.request<Company>(`${this.baseUrl}${id}/`, {
      method: 'PUT',
      body: JSON.stringify(companyData)
    });
  }

  async deleteCompany(id: string): Promise<{ message: string }> {
    return apiService.request<{ message: string }>(`${this.baseUrl}${id}/`, {
      method: 'DELETE'
    });
  }

  async assignDriverToCompany(companyId: string, driverId: string): Promise<{ message: string; company: Company }> {
    return apiService.request<{ message: string; company: Company }>(`${this.baseUrl}${companyId}/drivers/${driverId}/`, {
      method: 'POST'
    });
  }

  async removeDriverFromCompany(companyId: string, driverId: string): Promise<{ message: string; company: Company }> {
    return apiService.request<{ message: string; company: Company }>(`${this.baseUrl}${companyId}/drivers/${driverId}/`, {
      method: 'DELETE'
    });
  }

  async getAvailableDrivers(params?: {
    skip?: number;
    limit?: number;
  }): Promise<Driver[]> {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());

    const url = `${this.baseUrl}drivers/available/?${queryParams.toString()}`;
    return apiService.request<Driver[]>(url);
  }
}

export const companyService = new CompanyService(); 