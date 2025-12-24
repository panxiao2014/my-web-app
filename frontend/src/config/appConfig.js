import configData from '../../../config/app_config.json'

export const COMMON_CONFIG = configData.common
export const ZHONGKAO_CONFIG = configData.zhongkao

// Helper function to format page indicator text
export function formatPageIndicator(current, total) {
  return COMMON_CONFIG.navigation.pageIndicator
    .replace('{current}', current)
    .replace('{total}', total)
}