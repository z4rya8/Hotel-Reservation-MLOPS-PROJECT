import { useState } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { Hotel, Sparkles, Calendar, Users, CreditCard, Utensils, Bed } from "lucide-react";
import { toast } from "sonner";

type FormData = {
  lead_time: number;
  no_of_special_request: number;
  avg_price_per_room: number;
  arrival_month: string;
  arrival_date: string;
  market_segment_type: string;
  no_of_week_nights: number;
  no_of_weekend_nights: number;
  type_of_meal_plan: string;
  room_type_reserved: string;
};

const Index = () => {
  const [prediction, setPrediction] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { register, handleSubmit, setValue, formState: { errors } } = useForm<FormData>();

  const onSubmit = async (data: FormData) => {
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      // Mock prediction logic
      const randomPrediction = Math.random() > 0.5 ? 1 : 0;
      setPrediction(randomPrediction);
      setIsLoading(false);
      
      toast.success("Prediction completed!", {
        description: randomPrediction === 1 
          ? "Customer is likely to keep their reservation" 
          : "Customer may cancel their reservation"
      });
    }, 1500);
  };

  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  const marketSegments = [
    { value: "0", label: "Aviation" },
    { value: "1", label: "Complimentary" },
    { value: "2", label: "Corporate" },
    { value: "3", label: "Offline" },
    { value: "4", label: "Online" }
  ];

  const mealPlans = [
    { value: "0", label: "Meal Plan 1" },
    { value: "1", label: "Meal Plan 2" },
    { value: "2", label: "Meal Plan 3" },
    { value: "3", label: "Not Selected" }
  ];

  const roomTypes = [
    { value: "0", label: "Room Type 1" },
    { value: "1", label: "Room Type 2" },
    { value: "2", label: "Room Type 3" },
    { value: "3", label: "Room Type 4" },
    { value: "4", label: "Room Type 5" },
    { value: "5", label: "Room Type 6" },
    { value: "6", label: "Room Type 7" }
  ];

  return (
    <div className="min-h-screen bg-gradient-hero relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjEiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-20"></div>
      
      {/* Hero Section */}
      <div className="relative py-16 px-4">
        
        <div className="relative max-w-4xl mx-auto text-center animate-fade-in">
          <div className="inline-block p-3 bg-white/10 backdrop-blur-sm rounded-2xl mb-6 animate-float">
            <Hotel className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 tracking-tight">
            Hotel Reservation Prediction
          </h1>
          <p className="text-xl text-white/90 max-w-2xl mx-auto">
            Predict booking cancellations with AI-powered analytics
          </p>
        </div>
      </div>

      {/* Form Section */}
      <div className="relative max-w-5xl mx-auto px-4 -mt-8 pb-16">
        <Card className="shadow-luxury backdrop-blur-sm border-0 animate-scale-in">
          <CardContent className="p-8 md:p-12">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
              {/* Booking Details Section */}
              <div className="space-y-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-primary/10 rounded-lg">
                    <Calendar className="w-5 h-5 text-primary" />
                  </div>
                  <h2 className="text-2xl font-semibold text-foreground">Booking Details</h2>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2 group">
                    <Label htmlFor="lead_time" className="text-sm font-medium">Lead Time (days)</Label>
                    <Input
                      id="lead_time"
                      type="number"
                      placeholder="e.g., 30"
                      className="transition-all duration-300 focus:shadow-elegant"
                      {...register("lead_time", { required: true, valueAsNumber: true })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="no_of_special_request" className="text-sm font-medium">Special Requests</Label>
                    <Input
                      id="no_of_special_request"
                      type="number"
                      placeholder="e.g., 2"
                      className="transition-all duration-300 focus:shadow-elegant"
                      {...register("no_of_special_request", { required: true, valueAsNumber: true })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="arrival_month" className="text-sm font-medium">Arrival Month</Label>
                    <Select onValueChange={(value) => setValue("arrival_month", value)}>
                      <SelectTrigger className="transition-all duration-300 focus:shadow-elegant">
                        <SelectValue placeholder="Select month" />
                      </SelectTrigger>
                      <SelectContent className="bg-card">
                        {months.map((month, idx) => (
                          <SelectItem key={idx} value={(idx + 1).toString()}>
                            {month}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="arrival_date" className="text-sm font-medium">Arrival Date</Label>
                    <Select onValueChange={(value) => setValue("arrival_date", value)}>
                      <SelectTrigger className="transition-all duration-300 focus:shadow-elegant">
                        <SelectValue placeholder="Select date" />
                      </SelectTrigger>
                      <SelectContent className="bg-card">
                        {Array.from({ length: 31 }, (_, i) => i + 1).map((date) => (
                          <SelectItem key={date} value={date.toString()}>
                            {date}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              {/* Stay Details Section */}
              <div className="space-y-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-secondary/10 rounded-lg">
                    <Bed className="w-5 h-5 text-secondary" />
                  </div>
                  <h2 className="text-2xl font-semibold text-foreground">Stay Details</h2>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="no_of_week_nights" className="text-sm font-medium">Week Nights</Label>
                    <Input
                      id="no_of_week_nights"
                      type="number"
                      placeholder="e.g., 3"
                      className="transition-all duration-300 focus:shadow-elegant"
                      {...register("no_of_week_nights", { required: true, valueAsNumber: true })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="no_of_weekend_nights" className="text-sm font-medium">Weekend Nights</Label>
                    <Input
                      id="no_of_weekend_nights"
                      type="number"
                      placeholder="e.g., 2"
                      className="transition-all duration-300 focus:shadow-elegant"
                      {...register("no_of_weekend_nights", { required: true, valueAsNumber: true })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="room_type_reserved" className="text-sm font-medium">Room Type</Label>
                    <Select onValueChange={(value) => setValue("room_type_reserved", value)}>
                      <SelectTrigger className="transition-all duration-300 focus:shadow-elegant">
                        <SelectValue placeholder="Select room type" />
                      </SelectTrigger>
                      <SelectContent className="bg-card">
                        {roomTypes.map((room) => (
                          <SelectItem key={room.value} value={room.value}>
                            {room.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="avg_price_per_room" className="text-sm font-medium">Avg. Price per Room</Label>
                    <div className="relative">
                      <CreditCard className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                      <Input
                        id="avg_price_per_room"
                        type="number"
                        placeholder="e.g., 150"
                        className="pl-10 transition-all duration-300 focus:shadow-elegant"
                        {...register("avg_price_per_room", { required: true, valueAsNumber: true })}
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Guest Preferences Section */}
              <div className="space-y-6">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-accent/10 rounded-lg">
                    <Utensils className="w-5 h-5 text-accent" />
                  </div>
                  <h2 className="text-2xl font-semibold text-foreground">Guest Preferences</h2>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="type_of_meal_plan" className="text-sm font-medium">Meal Plan</Label>
                    <Select onValueChange={(value) => setValue("type_of_meal_plan", value)}>
                      <SelectTrigger className="transition-all duration-300 focus:shadow-elegant">
                        <SelectValue placeholder="Select meal plan" />
                      </SelectTrigger>
                      <SelectContent className="bg-card">
                        {mealPlans.map((meal) => (
                          <SelectItem key={meal.value} value={meal.value}>
                            {meal.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="market_segment_type" className="text-sm font-medium">Market Segment</Label>
                    <Select onValueChange={(value) => setValue("market_segment_type", value)}>
                      <SelectTrigger className="transition-all duration-300 focus:shadow-elegant">
                        <SelectValue placeholder="Select segment" />
                      </SelectTrigger>
                      <SelectContent className="bg-card">
                        {marketSegments.map((segment) => (
                          <SelectItem key={segment.value} value={segment.value}>
                            {segment.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full h-14 text-lg font-semibold bg-gradient-hero hover:shadow-glow transition-all duration-300 transform hover:scale-[1.02]"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-5 w-5" />
                    Predict Cancellation Risk
                  </>
                )}
              </Button>
            </form>

            {/* Results Section */}
            {prediction !== null && (
              <div className="mt-8 animate-scale-in">
                <Card className={`${
                  prediction === 0 
                    ? 'bg-destructive/5 border-destructive/20' 
                    : 'bg-secondary/5 border-secondary/20'
                } border-2 transition-all duration-300`}>
                  <CardContent className="p-6">
                    <div className="flex items-center gap-4">
                      <div className={`p-3 rounded-full ${
                        prediction === 0 ? 'bg-destructive/10' : 'bg-secondary/10'
                      }`}>
                        {prediction === 0 ? (
                          <svg className="w-8 h-8 text-destructive" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        ) : (
                          <svg className="w-8 h-8 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </div>
                      <div>
                        <h3 className="text-xl font-semibold mb-1">
                          {prediction === 0 ? 'High Cancellation Risk' : 'Low Cancellation Risk'}
                        </h3>
                        <p className="text-muted-foreground">
                          {prediction === 0 
                            ? 'The customer is likely to cancel their reservation' 
                            : 'The customer is likely to keep their reservation'}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Index;
