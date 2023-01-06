export interface ImageRequest {
  filename: string;
  url?: string;

  image: string;
  size: number;
  type: string;
  width: number;
  height: number;
}

export interface ImageResponse {
  filename: string;
  url?: string;
  timestamp: Date;
  model_version?: string;
  model_prediction?: number;
  model_is_ai_generated?: boolean;
}
