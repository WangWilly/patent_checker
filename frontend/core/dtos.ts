export type Product = {
  product_name: string;
  infringement_likelihood: string;
  relevant_claims: string[];
  explanation: string;
  specific_features: string[];
};

export type PatentInfringement = {
  patent_id: string;
  company_name: string;
  analysis_date: string;
  top_infringing_products: Product[];
  overall_risk_assessment: string;
};

////////////////////////////////////////////////////////////////////////////////

export type AssessInfringementV1 = {
  id: number;
  patent_id: string;
  company_name: string;
  analysis_date: string;
  top_infringing_products: Product[];
  overall_risk_assessment: string;
  created_at: string;
  updated_at: string;
};